import UploadZone from '@/components/library/UploadZone';
import DocumentList from '@/components/library/DocumentList';

export default function LibraryPage() {
  return (
    <div className="h-full w-full bg-[#020617] overflow-y-auto p-6 md:p-10 relative">
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-[#B200FF]/5 rounded-full blur-[150px] pointer-events-none"></div>
      
      <div className="max-w-5xl mx-auto space-y-8 relative z-10">
        <div>
          <h1 className="text-3xl font-bold text-slate-100 tracking-tight mb-2">Document Library</h1>
          <p className="text-slate-400">Manage your knowledge base and vector memory chunks.</p>
        </div>
        
        <UploadZone />
        <DocumentList />
      </div>
    </div>
  );
}
