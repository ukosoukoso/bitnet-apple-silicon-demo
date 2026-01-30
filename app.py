#!/usr/bin/env python3
"""BitNet Web UI using Gradio."""

import subprocess
import gradio as gr

MODEL_PATH = "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"
LLAMA_CLI = "./build/bin/llama-cli"

def generate_response(message, history):
    """Generate a response from BitNet."""
    
    # Build conversation history
    prompt = ""
    for user_msg, assistant_msg in history:
        prompt += f"Human: {user_msg}\n\nBITNETAssistant: {assistant_msg}\n\n"
    prompt += f"Human: {message}\n\nBITNETAssistant:"
    
    # Run llama-cli
    cmd = [
        LLAMA_CLI,
        "-m", MODEL_PATH,
        "-p", prompt,
        "-n", "200",
        "-t", "8",
        "--repeat-penalty", "1.5",
        "--temp", "0.7",
        "--top-p", "0.9",
        "--no-warmup",
        "-e",
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        output = result.stdout + result.stderr
        
        # Extract response
        if "BITNETAssistant:" in output:
            parts = output.split("BITNETAssistant:")
            response = parts[-1].strip()
            
            # Clean up
            lines = []
            for line in response.split('\n'):
                if line.startswith('llama_perf') or line.startswith('ggml_'):
                    break
                lines.append(line)
            response = '\n'.join(lines).strip()
            response = response.replace('[end of text]', '').strip()
            
            if len(response) > 1000:
                response = response[:1000] + "..."
                
            return response if response else "..."
        return "..."
        
    except subprocess.TimeoutExpired:
        return "[Timeout]"
    except Exception as e:
        return f"[Error: {e}]"

# Create Gradio interface
demo = gr.ChatInterface(
    fn=generate_response,
    title="🧠 BitNet 1-bit LLM",
    description="Running Microsoft BitNet b1.58 2B on Apple Silicon (CPU only)",
    examples=[
        "Hello! What can you do?",
        "Explain quantum computing in simple terms",
        "Write a haiku about coding",
    ],
    theme=gr.themes.Soft(),
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
