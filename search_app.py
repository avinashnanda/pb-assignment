import gradio as gr
import requests
import base64
from io import BytesIO
from PIL import Image

API_URL = "http://127.0.0.1:8000/search"

def base64_to_image(base64_str):
    """Convert base64 string to PIL image."""
    image_data = base64.b64decode(base64_str)
    return Image.open(BytesIO(image_data))

def search_images(query, k):
    payload = {"query": query, "k": k}
    resp = requests.post(API_URL, json=payload)

    if resp.status_code != 200:
        return ["Error fetching results. Check API backend is running."]

    results = resp.json()

    # Build HTML collage with image + explanation card
    html_blocks = ""
    for r in results:
        explanation = r.get("explanation", "No explanation provided.")
        score = round(r.get("score", 0), 3)
        img_base64 = r["image_base64"]

        html_blocks += f"""
        <div style="display:flex;align-items:center;margin-bottom:20px;
                    padding:10px;border-radius:12px;
                    box-shadow:0 2px 6px rgba(0,0,0,0.1)">
            <div style="flex:1;padding-right:15px">
                <img src="data:image/png;base64,{img_base64}" 
                     style="max-width:100%;border-radius:10px"/>
            </div>
            <div style="flex:2;background:#fafafa;padding:15px;border-radius:10px">
                <h3 style="margin-top:0">📝 Explanation</h3>
                <p>{explanation}</p>
                <p><b>📊 Score:</b> {score}</p>
            </div>
        </div>
        """

    return html_blocks


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## AI-Powered Image Semantic Search")
    gr.Markdown("Search images using natural language queries, with **AI explanations**.")

    with gr.Row():
        query_in = gr.Textbox(label="Enter your query", placeholder="e.g., a dog playing in the park")
        k_in = gr.Slider(1, 10, value=3, step=1, label="Number of results")
        search_btn = gr.Button("🔎 Search")

    results_output = gr.HTML()

    search_btn.click(
        fn=search_images,
        inputs=[query_in, k_in],
        outputs=results_output
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860,pwa=True)
