import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def get_accuracy(df_true: pd.DataFrame, df_pred: pd.DataFrame) -> float:
    return accuracy_score(df_true['ground_truth_intent'], df_pred['predicted_intent'])

def get_precision(df_true: pd.DataFrame, df_pred: pd.DataFrame) -> float:
    return precision_score(df_true['ground_truth_intent'], df_pred['predicted_intent'], average='micro')

def get_recall(df_true: pd.DataFrame, df_pred: pd.DataFrame) -> float:
    return recall_score(df_true['ground_truth_intent'], df_pred['predicted_intent'], average='micro')

def get_f1(df_true: pd.DataFrame, df_pred: pd.DataFrame) -> float:
    return f1_score(df_true['ground_truth_intent'], df_pred['predicted_intent'], average='micro')

if __name__ == '__main__':
    df_true = pd.read_excel('/Users/tjain1/Desktop/sides/Zendesk/data/intents_accuracy_data/ground_truth_intent_dialogues.xlsx')
    df_pred = pd.read_excel('/Users/tjain1/Desktop/sides/Zendesk/data/intents_accuracy_data/predicted_intents.xlsx')

    print(f"Action classification accuracy:{get_accuracy(df_true, df_pred)})")
    print(f"Action classification precision:{get_precision(df_true, df_pred)})")
    print(f"Action classification recall:{get_recall(df_true, df_pred)})")
    print(f"Action classification f1 score:{get_f1(df_true, df_pred)})")

    print(f"Where prediction varies from ground truth intent:\n"
          f"{df_pred[df_pred['predicted_intent'] != df_true['ground_truth_intent']]['dialogues'].values})")