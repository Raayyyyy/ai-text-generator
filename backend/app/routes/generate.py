from flask import Blueprint, request, jsonify, current_app
import openai
import json

bp = Blueprint('generate', __name__, url_prefix='/api/generate')

def get_openai_client():
    """获取OpenAI客户端实例"""
    api_key = current_app.config['OPENAI_API_KEY']
    api_base = current_app.config['OPENAI_API_BASE']
    
    if not api_key or api_key == 'your-api-key-here':
        raise Exception("请配置有效的OpenAI API密钥")
    
    openai.api_key = api_key
    if api_base:
        openai.api_base = api_base
    
    return openai

def get_style_prompt(style, language='zh'):
    """获取不同风格的提示词"""
    style_prompts = {
        'academic': {
            'zh': """
- 使用学术性的词汇和表达
- 保持客观和严谨的语气
- 适当引用和论证
- 使用专业术语
- 结构化的段落组织
- 避免过于口语化的表达""",
            'en': """
- Use academic vocabulary and expressions
- Maintain objective and rigorous tone
- Include appropriate citations and arguments
- Use professional terminology
- Structured paragraph organization
- Avoid colloquial expressions"""
        },
        'business': {
            'zh': """
- 使用商务专业用语
- 保持简洁清晰的表达
- 注重逻辑性和说服力
- 适当使用数据支持
- 保持礼貌专业的语气
- 强调关键点和结论""",
            'en': """
- Use business terminology
- Keep expressions concise and clear
- Focus on logic and persuasiveness
- Use data support appropriately
- Maintain polite and professional tone
- Emphasize key points and conclusions"""
        },
        'casual': {
            'zh': """
- 使用日常口语表达
- 加入口头禅和语气词
- 保持轻松自然的语气
- 可以使用简单的比喻
- 适当使用网络用语
- 语句结构灵活自然""",
            'en': """
- Use everyday expressions
- Include conversational fillers
- Maintain a relaxed and natural tone
- Use simple metaphors
- Include appropriate internet slang
- Flexible and natural sentence structure"""
        },
        'humorous': {
            'zh': """
- 添加幽默元素和双关语
- 使用生动的比喻
- 适当夸张和调侃
- 保持轻松愉快的语气
- 可以使用俏皮话
- 注意幽默的分寸""",
            'en': """
- Add humor elements and wordplay
- Use vivid metaphors
- Appropriate exaggeration and teasing
- Maintain a light and fun tone
- Include witty remarks
- Mind the degree of humor"""
        },
        'narrative': {
            'zh': """
- 采用故事化的叙述方式
- 添加细节和场景描写
- 注重情节的流畅性
- 可以加入对话元素
- 营造适当的氛围
- 突出人物和情感""",
            'en': """
- Use storytelling narrative
- Add details and scene descriptions
- Focus on plot fluency
- Include dialogue elements
- Create appropriate atmosphere
- Emphasize characters and emotions"""
        },
        'journalistic': {
            'zh': """
- 使用新闻报道的语气
- 强调客观性和时效性
- 遵循倒金字塔结构
- 突出关键信息
- 使用引用和数据
- 保持专业的报道风格""",
            'en': """
- Use journalistic tone
- Emphasize objectivity and timeliness
- Follow inverted pyramid structure
- Highlight key information
- Use quotes and data
- Maintain professional reporting style"""
        },
        'blog': {
            'zh': """
- 个人化的写作风格
- 加入个人观点和经历
- 与读者互动的语气
- 使用生活化的例子
- 保持轻松但有见地
- 可以展现个性""",
            'en': """
- Personal writing style
- Include personal views and experiences
- Interactive tone with readers
- Use real-life examples
- Keep it casual but insightful
- Show personality"""
        },
        'social': {
            'zh': """
- 简短有力的表达
- 使用流行语和话题标签
- 互动性强的语气
- 可以使用表情符号
- 注重分享性和传播性
- 紧跟热点话题""",
            'en': """
- Short and powerful expressions
- Use trending terms and hashtags
- Highly interactive tone
- Can use emojis
- Focus on shareability
- Follow trending topics"""
        }
    }
    return style_prompts.get(style, {}).get(language, style_prompts['casual'][language])

def get_prompt_by_mode(mode, strength_text, strength, language='zh', style=None):
    """根据模式和语言返回对应的prompt"""
    if mode == 'rewrite':
        if language == 'zh':
            return f"""你是一个专业的文本改写助手。请对输入的文本进行{strength_text}程度的改写。
要求：
1. 保持原文的核心意思不变
2. 使用同义词替换和句式重组
3. 确保输出流畅自然
4. 改写程度大约在{int(strength*100)}%左右
5. 输出必须是中文"""
        else:
            return f"""You are a professional text rewriting assistant. Please rewrite the input text with {strength_text} modification.
Requirements:
1. Maintain the core meaning of the original text
2. Use synonyms and sentence restructuring
3. Ensure the output is fluent and natural
4. The rewrite rate should be around {int(strength*100)}%
5. Output must be in English"""
    else:  # humanize mode
        if language == 'zh':
            return f"""你是一个专业的AI文本人性化专家。你的任务是让输入的文本听起来更自然、更像人类写的。
要求：
1. 保持原文的核心信息和含义
2. 使用以下技巧，程度为{strength_text}：
   - 添加自然的语言变化和不完美性
   - 加入对话元素和过渡词
   - 使用更口语化的表达
   - 变化句子结构和长度
   - 添加适当的语气词和停顿
   - 融入个人语气和视角
3. 修改程度大约在{int(strength*100)}%
4. 确保输出专业的同时更像人类写作
5. 避免过于完美或机械的语言模式
6. 输出必须是中文"""
        else:
            return f"""You are an expert in humanizing AI-generated text. Your task is to make the input text sound more natural and human-like.
Requirements:
1. Maintain the core information and meaning
2. Apply the following techniques with {strength_text} intensity:
   - Add natural language variations and imperfections
   - Include conversational elements and transitions
   - Use more casual and human-like expressions
   - Vary sentence structure and length
   - Add appropriate filler words and hesitations
   - Incorporate personal tone and perspective
3. The modification level should be around {int(strength*100)}%
4. Ensure the output remains professional while sounding more human-written
5. Avoid overly perfect or mechanical language patterns
6. Output must be in English"""

    # 如果是人性化模式且指定了风格，添加风格相关的提示词
    if mode == 'humanize' and style:
        base_prompt += "\n\n特定风格要求：" if language == 'zh' else "\n\nStyle-specific requirements:"
        base_prompt += get_style_prompt(style, language)

    return base_prompt

def reduce_ai_text(text, strength=0.5, use_advanced=False, model="gpt-3.5-turbo", mode="rewrite", language='zh', style=None):
    """使用OpenAI API的文本处理函数"""
    try:
        client = get_openai_client()
        
        # 验证模型名称
        valid_models = {
            'gpt-3.5-turbo': {'max_tokens': 4000},
            'gpt-3.5-turbo-16k': {'max_tokens': 16000},
            'gpt-4': {'max_tokens': 8000},
            'gpt-4-turbo-preview': {'max_tokens': 4000}
        }
        
        if model not in valid_models:
            raise Exception("不支持的模型类型")
        
        # 获取提示词
        strength_text = "mild" if strength < 0.3 else "moderate" if strength < 0.7 else "strong"
        system_prompt = get_prompt_by_mode(mode, strength_text, strength, language, style)
        
        print(f"\n=== Using Model: {model} ===")
        print(f"=== Mode: {mode} ===")
        
        # 使用新版本的 API 调用方式
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Please process the following text:\n{text}"}
            ],
            temperature=0.7,
            max_tokens=valid_models[model]['max_tokens'],
            top_p=0.9,
            frequency_penalty=0.6,
            presence_penalty=0.6
        )
        
        processed_text = response.choices[0].message.content.strip()
        return processed_text
        
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        if "API key" in str(e):
            raise Exception("OpenAI API 密钥无效")
        raise Exception(f"AI处理失败: {str(e)}")

@bp.route('', methods=['POST'])
def generate_text():
    try:
        print("收到请求")
        data = request.get_json()
        print("请求数据:", data)
        
        if not data or 'text' not in data:
            print("错误：没有提供文本")
            return jsonify({'error': '请提供文本'}), 400
        
        # 检查 API 密钥
        api_key = current_app.config['OPENAI_API_KEY']
        print("API Key configured:", bool(api_key))  # 打印 API 密钥状态
        
        if not api_key:
            print("错误：未配置 OpenAI API 密钥")
            return jsonify({'error': '未配置 OpenAI API 密钥'}), 500
            
        text = data['text']
        strength = data.get('strength', 0.5)
        use_advanced = data.get('advanced', False)
        model = data.get('model', 'gpt-3.5-turbo')
        mode = data.get('mode', 'rewrite')
        language = data.get('language', 'zh')
        style = data.get('style') if data.get('mode') == 'humanize' else None
        
        print(f"处理参数: text={text}, strength={strength}, advanced={use_advanced}, model={model}, mode={mode}, language={language}, style={style}")
        
        try:
            processed_text = reduce_ai_text(text, strength, use_advanced, model, mode, language, style)
            print("处理结果:", processed_text)
            
            return jsonify({
                'processed': processed_text,
                'original': text,
                'model': model,
                'mode': mode,
                'language': language
            })
        except Exception as e:
            print("AI处理错误:", str(e))
            return jsonify({'error': f"AI处理错误: {str(e)}"}), 500
            
    except Exception as e:
        print("请求处理错误:", str(e))
        error_message = str(e)
        if "API key" in error_message:
            error_message = "OpenAI API 密钥无效或未配置"
        return jsonify({'error': error_message}), 500