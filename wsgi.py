from flask import Flask, render_template, request, jsonify
from ai_schematic_generator.ai_generator import AISchematicGenerator
import os

app = Flask(__name__)
api_key = os.getenv('ANTHROPIC_API_KEY')
generator = AISchematicGenerator(api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
async def generate():
    description = request.json.get('description')
    output_file = f"static/schematics/{description[:10]}.svg"
    
    try:
        result = await generator.generate_schematic_from_description(
            description,
            output_file
        )
        return jsonify({'success': True, 'file': output_file})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
