import openai

# --- CONFIGURATION GROQ (GRATUIT) ---
# Ta clé est maintenant intégrée ici
api_key = 

client = openai.OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1" # <--- Connexion au serveur gratuit
)

def parler_a_oracle():
    print("\n" + "="*30)
    print("   ORACLE EST EN LIGNE (GROQ)")
    print("="*30)
    print("Tape 'quitter' pour sortir.\n")
    
    # Instruction système pour définir la personnalité de luxe
    messages = [
        {"role": "system", "content": "Tu es ORACLE. Un mentor secret, incisif et élégant. Tu analyses le charisme et la persuasion de l'utilisateur. Ton ton est froid et prestigieux. Ne fais pas de phrases inutiles."}
    ]

    while True:
        user_input = input("Toi > ")
        
        if user_input.lower() in ["quitter", "exit", "stop"]:
            print("\nORACLE > La session est terminée. Travaille ton impact.")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            # Appel à l'IA (Utilisation du modèle Llama 3 sur Groq)
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile", # <--- Modèle surpuissant et gratuit
                messages=messages
            )
            
            reponse_oracle = response.choices[0].message.content
            print(f"\nORACLE > {reponse_oracle}\n")
            messages.append({"role": "assistant", "content": reponse_oracle})
            
        except Exception as e:
            print(f"\n[ERREUR] Oracle a rencontré un problème : {e}")
            break

if __name__ == "__main__":
    parler_a_oracle()