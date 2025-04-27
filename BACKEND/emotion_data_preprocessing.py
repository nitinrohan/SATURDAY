import pandas as pd

# Load GoEmotions datasets
df_go1 = pd.read_csv("DATASETS/GoEmotions/data/full_dataset/goemotions_1.csv")
df_go2 = pd.read_csv("DATASETS/GoEmotions/data/full_dataset/goemotions_2.csv")
df_go3 = pd.read_csv("DATASETS/GoEmotions/data/full_dataset/goemotions_3.csv")

# Combine into one dataframe
df = pd.concat([df_go1, df_go2, df_go3])

# List of emotion columns
emotion_columns = ['admiration', 'amusement', 'anger', 'annoyance', 'approval',
                   'caring', 'confusion', 'curiosity', 'desire', 'disappointment',
                   'disapproval', 'disgust', 'embarrassment', 'excitement', 'fear',
                   'gratitude', 'grief', 'joy', 'love', 'nervousness', 'optimism',
                   'pride', 'realization', 'relief', 'remorse', 'sadness', 'surprise', 'neutral']

# Melt to long format
df_melted = df.melt(
    id_vars=["text"],
    value_vars=emotion_columns,
    var_name="label",
    value_name="is_present"
)

# Only keep rows where emotion is present (is_present == 1)
df_final = df_melted[df_melted["is_present"] == 1][["text", "label"]]

# Shuffle
df_final = df_final.sample(frac=1).reset_index(drop=True)

# Save to CSV
df_final.to_csv("DATASETS/goemotions_only.csv", index=False)
print("✅ GoEmotions-only dataset saved as goemotions_only.csv")
