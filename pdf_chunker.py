import pdfplumber
import re

def read_pdf_with_layout(file_path):
    """用 pdfplumber 提取文本，保留换行和布局"""
    full_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
    return full_text

def smart_chunk_resume(text):
    """智能切分简历 - 修复版"""
    # 按双换行切分（段落分隔）
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    # 如果没有双换行，按单换行切分
    if len(paragraphs) <= 1:
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    
    # 过滤太短的段落（可能是噪声）
    paragraphs = [p for p in paragraphs if len(p) > 10]
    
    # 每个独立段落作为一个 chunk
    result = []
    for i, para in enumerate(paragraphs):
        # 第一段作为"个人信息"
        if i == 0:
            heading = "个人信息"
        else:
            # 尝试从段落开头提取标题（取前15字）
            heading = para[:15].strip()
            # 如果以常见关键词开头，截取关键词作为标题
            for keyword in ['教育', '工作', '技能', '项目', '语言', '证书', '获奖', '自我']:
                if para.startswith(keyword):
                    heading = keyword
                    break
        
        # 截取内容前500字
        content = para[:500] if len(para) > 500 else para
        result.append({"heading": heading, "content": content})
    
    # 如果段落太少（≤2），尝试按行切分
    if len(result) <= 2:
        lines = [l.strip() for l in text.split('\n') if l.strip() and len(l.strip()) > 15]
        result = []
        for i, line in enumerate(lines[:8]):
            heading = line[:15] if i > 0 else "个人信息"
            result.append({"heading": heading, "content": line[:500]})
    
    return result

if __name__ == "__main__":
    pdf_path = input("请输入PDF文件路径: ")
    text = read_pdf_with_layout(pdf_path)
    
    if not text.strip():
        print("警告: PDF 未提取到任何文本")
    else:
        print(f"提取到 {len(text)} 字符")
        chunks = smart_chunk_resume(text)
        print(f"共切出 {len(chunks)} 个段落\n")
        
        for i, chunk in enumerate(chunks):
            print(f"【段落{i+1}】{chunk['heading']}")
            print(f"{chunk['content'][:200]}")
            print("-" * 50)