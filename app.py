
import json
import streamlit as st
import sys
from openai import OpenAI

st.set_page_config(page_title="SNS要注意サイン診断",page_icon="⚠️")

client = OpenAI()

st.title("⚠️SNS要注意サイン診断⚠️")
st.write("メッセージ内容をAIが読み取り危険度と注意ポイントを判定します。")

text = st.text_area("ここにメッセージを貼る",height=220)

def ai_check_risk(text: str):
    prompt = f"""
あなたはSNS安全アドバイザーです。次のメッセージを読み、人物を断定評価せず、文章内の注意サインだけを分析してください。
出力は必ずjsonのみで返してください。
形式:
{{
  "risk":"低"または"中"または"高",
  "flags":["注意ポイント1","注意ポイント2"],
  "advice" "短い助言"
  "category":"詐欺" または "性的リスク" または "操作的言動" または "その他"
}}

判定基準:
-金銭的要求、投資、副業勧誘、外部アプリ誘導、秘密の強要、過度な親密さ、脅し、罪悪感での操作は危険度を上げる
-強い注意サインがなければ risk は「低」
-性的な話題そのものを自動で危険認定しない
-ただし、以下は危険度を上げる:
  -急な性的要求
  -裸の写真や動画の要求
  -断っても続く性的な要求
  -会う前の露骨な性的発言
  -会う前の露骨な性的誘導
  -秘密を求める性的会話
  -脅しや拡散を示唆する性的要求
  -年齢不明または未成年の可能性がある相手への性的接触
-強い注意サインが複数ある場合は「高」
-一つだけなら「中」の候補
-特に強い注意サインがなければ「低」
-人を断定せず、「注意が必要な表現がある」形式で書く

出力ルール
- flags は短く分かりやすく
- advice はユーザーがすぐ使える実用的な一文にする
- category は最も近いものを一つ選ぶ

対象メッセージ:
{text}
"""
    
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )

    raw = response.output_text
    data = json.loads(raw)
    return data


if st.button("🔍診断する"):
    if not text. strip():
        st.warning("入力してください")
    else:
        try:
            result = ai_check_risk(text) 

            st.subheader("診断結果")
            risk = result["risk"]

            if risk =="低":
                 st.success("🟢危険度：低")
            elif risk =="中":
                 st.warning("🟡危険度：中")
            else:
                 st.error("🔴危険度：高")

            st.subheader("注意ポイント")
            flags = result.get("flags",[])
            if flags:
                for f in flags:
                    st.write("・", f)
            else:
                st.write("特に強い注意サインは見つかりませんでした")

                

            st.subheader("アドバイス")
            st.info(result.get("advice","違和感がある場合は慎重に対応してください。"))  
                
        except Exception as e:
            st.error(f"エラーが発生しました:{e}")