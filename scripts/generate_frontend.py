import os

base = r"c:\Users\HP\Desktop\project\ATLAS1\frontend"
files = [
    r"app\chat\page.tsx",
    r"app\library\page.tsx",
    r"app\search\page.tsx",
    r"app\dashboard\page.tsx",
    r"app\settings\page.tsx",
    r"components\chat\ChatWindow.tsx",
    r"components\chat\MessageBubble.tsx",
    r"components\chat\SourceCitations.tsx",
    r"components\chat\StreamingCursor.tsx",
    r"components\chat\ContextBar.tsx",
    r"components\library\DocumentUploader.tsx",
    r"components\library\DocumentCard.tsx",
    r"components\library\IngestionProgress.tsx",
    r"components\dashboard\CompressionGauge.tsx",
    r"components\dashboard\MemoryWaterfall.tsx",
    r"components\dashboard\IndexStats.tsx",
    r"components\shared\Sidebar.tsx",
    r"components\shared\Header.tsx",
    r"components\shared\LoadingSpinner.tsx",
    r"lib\api.ts",
    r"lib\stores\chatStore.ts",
    r"lib\stores\libraryStore.ts",
    r"lib\types.ts",
]

for f in files:
    path = os.path.join(base, f)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fw:
        if f.endswith(".tsx"):
            name = os.path.basename(f).split(".")[0]
            if name == "page":
                name = os.path.basename(os.path.dirname(f)).capitalize() + "Page"
            fw.write(f"export default function {name}() {{\n  return <div className=\"p-4\">{name} component initialized</div>;\n}}\n")
        else:
            fw.write("// " + f + "\n")

print("Frontend structure generated successfully.")
