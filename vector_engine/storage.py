import mmap
import os
import struct
import numpy as np
from core.turboquant import TurboQuantVector

class TQVSWriter:
    def __init__(self, index_dir: str, filename: str = "index.tqvs"):
        os.makedirs(index_dir, exist_ok=True)
        self.filepath = os.path.join(index_dir, filename)
        # format: magic, version, num_vectors, d, bits, m
        self.header_fmt = "<4sIIIII40x"  # 64 bytes total
        self.meta_fmt = "<16s16seeI"     # 40 bytes: chunk_id(16), doc_id(16), norm(f16), r_final(f16), timestamp(I)
        
        self.num_vectors = 0
        self.d = 0
        self.bits = 0
        self.m = 0
        
        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) >= 64:
            with open(self.filepath, "rb") as f:
                header = f.read(64)
                magic, version, self.num_vectors, self.d, self.bits, self.m = struct.unpack(self.header_fmt, header)
                    
    def append(self, tqv: TurboQuantVector, chunk_id: str, doc_id: str, timestamp: int = 0):
        polar_bits = tqv.bits - 1
        angle_bytes = int(np.ceil((tqv.d - 1) * polar_bits / 8))
        sketch_bytes = len(tqv.qjl_sketch)
        
        if not os.path.exists(self.filepath) or os.path.getsize(self.filepath) == 0:
            self.d = tqv.d
            self.bits = tqv.bits
            self.m = sketch_bytes
            with open(self.filepath, "wb") as f:
                header = struct.pack(self.header_fmt, b"TQVS", 1, 0, self.d, self.bits, self.m)
                f.write(header)
                
        with open(self.filepath, "r+b") as f:
            chunk_bytes = chunk_id.encode('utf-8')[:16].ljust(16, b'\0')
            doc_bytes = doc_id.encode('utf-8')[:16].ljust(16, b'\0')
            meta_block = struct.pack(self.meta_fmt, chunk_bytes, doc_bytes, 
                                     np.float16(tqv.norm), np.float16(tqv.r_final), timestamp)
            
            f.seek(0, 2)
            f.write(meta_block)
            f.write(tqv.angle_indices.tobytes())
            f.write(tqv.qjl_sketch.tobytes())
            
            self.num_vectors += 1
            f.seek(8)
            f.write(struct.pack("<I", self.num_vectors))

class TQVSReader:
    def __init__(self, index_dir: str, filename: str = "index.tqvs"):
        self.filepath = os.path.join(index_dir, filename)
        self.header_fmt = "<4sIIIII40x"
        self.meta_fmt = "<16s16seeI"
        self.meta_size = struct.calcsize(self.meta_fmt)
        
        self.num_vectors = 0
        self.d = 0
        self.bits = 0
        self.m = 0
        
        if os.path.exists(self.filepath) and os.path.getsize(self.filepath) >= 64:
            with open(self.filepath, "rb") as f:
                header = f.read(64)
                magic, version, self.num_vectors, self.d, self.bits, self.m = struct.unpack(self.header_fmt, header)
                    
            polar_bits = self.bits - 1
            self.angle_bytes = int(np.ceil((self.d - 1) * polar_bits / 8))
            self.data_size = self.angle_bytes + self.m
            self.record_size = self.meta_size + self.data_size
            
            self.file_obj = open(self.filepath, "rb")
            self.mmap_obj = mmap.mmap(self.file_obj.fileno(), 0, access=mmap.ACCESS_READ)
        else:
            self.mmap_obj = None

    def get(self, idx: int) -> TurboQuantVector:
        if self.mmap_obj is None or idx >= self.num_vectors:
            raise IndexError("Vector index out of bounds")
            
        offset = 64 + idx * self.record_size
        meta_bytes = self.mmap_obj[offset : offset + self.meta_size]
        chunk_b, doc_b, norm_f16, r_final_f16, timestamp = struct.unpack(self.meta_fmt, meta_bytes)
        
        data_offset = offset + self.meta_size
        angle_bytes_data = self.mmap_obj[data_offset : data_offset + self.angle_bytes]
        sketch_bytes_data = self.mmap_obj[data_offset + self.angle_bytes : data_offset + self.data_size]
        
        return TurboQuantVector(
            norm=float(norm_f16),
            r_final=float(r_final_f16),
            angle_indices=np.frombuffer(angle_bytes_data, dtype=np.uint8),
            qjl_sketch=np.frombuffer(sketch_bytes_data, dtype=np.int8),
            d=self.d,
            bits=self.bits
        )

    def get_metadata(self, idx: int) -> tuple[str, str]:
        offset = 64 + idx * self.record_size
        meta_bytes = self.mmap_obj[offset : offset + self.meta_size]
        chunk_b, doc_b, _, _, _ = struct.unpack(self.meta_fmt, meta_bytes)
        chunk_id = chunk_b.decode('utf-8').rstrip('\0')
        doc_id = doc_b.decode('utf-8').rstrip('\0')
        return chunk_id, doc_id
        
    def is_deleted(self, idx: int) -> bool:
        return False
        
    def close(self):
        if self.mmap_obj:
            self.mmap_obj.close()
            self.file_obj.close()
