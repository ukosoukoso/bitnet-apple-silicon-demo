#!/usr/bin/env python3
"""Simple multi-turn chat script for BitNet model."""

import subprocess
import sys
import re

MODEL_PATH = "models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf"
LLAMA_CLI = "./build/bin/llama-cli"

def extract_response(output, user_content):
    """Extract the assistant's response from llama-cli output."""
    # Find the actual generated text after the prompt
    # The output format is: prompt + generated_text + perf_stats
    
    # Remove all lines starting with common prefixes
    lines = output.split('\n')
    filtered_lines = []
    skip_prefixes = ('llama_', 'ggml_', 'llm_load', 'main:', 'build:', 'sampler', 
                     'generate:', 'common_', 'check_double', '\t', 'system_info')
    
    in_output = False
    for line in lines:
        # Skip metadata/loading lines
        if any(line.strip().startswith(p) for p in skip_prefixes):
            continue
        # Skip empty lines at the start
        if not in_output and not line.strip():
            continue
        # Stop at performance stats
        if 'llama_perf' in line or 'tokens per second' in line:
            break
        in_output = True
        filtered_lines.append(line)
    
    text = '\n'.join(filtered_lines).strip()
    
    # Find the response after BITNETAssistant:
    if "BITNETAssistant:" in text:
        parts = text.split("BITNETAssistant:")
        response = parts[-1].strip()
    else:
        response = text
    
    # Clean up
    response = response.replace('[end of text]', '').strip()
    response = re.sub(r'\s*Human:\s*$', '', response)  # Remove trailing "Human:"
    
    return response

def chat():
    history = []
    print("=" * 50)
    print("  BitNet 多轮对话")
    print("  输入 'quit' 或 'exit' 退出")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\n你: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n再见! 👋")
            break
            
        if not user_input:
            continue
        if user_input.lower() in ('quit', 'exit', 'q'):
            print("\n再见! 👋")
            break
        
        # Build conversation history
        history.append({"role": "user", "content": user_input})
        
        # Format prompt using the model's chat template
        prompt = ""
        for msg in history:
            if msg["role"] == "user":
                prompt += f"Human: {msg['content']}\n\nBITNETAssistant:"
            else:
                prompt += f" {msg['content']}\n\n"
        
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
            "-e",  # escape sequences
        ]
        
        print("\nBitNet: ", end="", flush=True)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            output = result.stdout + result.stderr
            response = extract_response(output, user_input)
            
            if response:
                # Limit response to avoid runaway generation
                if len(response) > 1000:
                    response = response[:1000] + "..."
                print(response)
                history.append({"role": "assistant", "content": response})
            else:
                print("[无响应]")
                
        except subprocess.TimeoutExpired:
            print("[超时]")
        except Exception as e:
            print(f"[错误: {e}]")

if __name__ == "__main__":
    chat()
