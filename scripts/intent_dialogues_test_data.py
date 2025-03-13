import pandas as pd
from pathlib import Path

SRC_DIR_TRACK = Path('../data/gold_dataset/track')
SRC_DIR_CANCEL = Path('../data/gold_dataset/cancel')
TARGET_DIR = Path('../data')

def split_conversations(file: Path) -> pd.DataFrame:
    with open(file, 'r') as f:
        file_content = f.read()

    all_dialogues = file_content.split('\n')
    dialogues_built = []
    for i in range(len(all_dialogues)):
        if all_dialogues[i].startswith('User'):
            dialogues_built.append('\n'.join(all_dialogues[:i + 1]))
    dialogues_built.append('\n'.join(all_dialogues))

    return pd.DataFrame({'dialogues': dialogues_built, 'file_name': file.name})

if __name__ == '__main__':
    if not TARGET_DIR.exists():
        TARGET_DIR.mkdir()

    df = pd.DataFrame(columns=['dialogues', 'file_name'])
    for file in SRC_DIR_TRACK.iterdir():
        df = pd.concat([df, split_conversations(file)])

    for file in SRC_DIR_CANCEL.iterdir():
        df = pd.concat([df, split_conversations(file)])

    df = df.reset_index(drop='index')
    df.to_excel(TARGET_DIR / 'ground_truth_intent_dialogues.xlsx', index=None)