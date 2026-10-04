from __future__ import annotations

import argparse

from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold
from sklearn.tree import DecisionTreeClassifier

from config import REPORTS_DIR
from training_utils import build_pipeline, load_training_frame, save_json, split_data
from training_utils import artifact_dir, save_model


def main() -> None:
    parser = argparse.ArgumentParser(description="Tune NeuroPulse classifiers with cross-validation.")
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--n-iter", type=int, default=12)
    args = parser.parse_args()

    frame = load_training_frame()
    split = split_data(frame, random_state=args.random_state)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=args.random_state)

    tuning_results: dict[str, object] = {}

    decision_tree_grid = {
        "model__criterion": ["gini", "entropy"],
        "model__max_depth": [3, 4, 5, 6, 8, None],
        "model__min_samples_split": [2, 5, 10, 20],
        "model__min_samples_leaf": [1, 2, 4, 8],
    }
    decision_tree_search = GridSearchCV(
        build_pipeline(DecisionTreeClassifier(random_state=args.random_state, class_weight="balanced")),
        decision_tree_grid,
        scoring="f1_macro",
        cv=cv,
        n_jobs=-1,
    )
    decision_tree_search.fit(split.x_train, split.y_train)
    save_model(artifact_dir() / "decision_tree_tuned.joblib", decision_tree_search.best_estimator_)
    tuning_results["decision_tree"] = {
        "best_score": float(decision_tree_search.best_score_),
        "best_params": decision_tree_search.best_params_,
    }

    random_forest_grid = {
        "model__n_estimators": [150, 200, 300, 400],
        "model__max_depth": [None, 6, 10, 14],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "model__max_features": ["sqrt", "log2", None],
    }
    random_forest_search = RandomizedSearchCV(
        build_pipeline(RandomForestClassifier(random_state=args.random_state, class_weight="balanced", n_jobs=-1)),
        random_forest_grid,
        n_iter=args.n_iter,
        scoring="f1_macro",
        cv=cv,
        n_jobs=-1,
        random_state=args.random_state,
    )
    random_forest_search.fit(split.x_train, split.y_train)
    save_model(artifact_dir() / "random_forest_tuned.joblib", random_forest_search.best_estimator_)
    tuning_results["random_forest"] = {
        "best_score": float(random_forest_search.best_score_),
        "best_params": random_forest_search.best_params_,
    }

    extra_trees_grid = {
        "model__n_estimators": [150, 250, 350, 450],
        "model__max_depth": [None, 8, 12, 16],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
    }
    extra_trees_search = RandomizedSearchCV(
        build_pipeline(ExtraTreesClassifier(random_state=args.random_state, class_weight="balanced", n_jobs=-1)),
        extra_trees_grid,
        n_iter=args.n_iter,
        scoring="f1_macro",
        cv=cv,
        n_jobs=-1,
        random_state=args.random_state,
    )
    extra_trees_search.fit(split.x_train, split.y_train)
    save_model(artifact_dir() / "extra_trees_tuned.joblib", extra_trees_search.best_estimator_)
    tuning_results["extra_trees"] = {
        "best_score": float(extra_trees_search.best_score_),
        "best_params": extra_trees_search.best_params_,
    }

    save_json(REPORTS_DIR / "hyperparameter_tuning_summary.json", tuning_results)
    print("Saved tuning summary to backend/ml/reports/hyperparameter_tuning_summary.json")


if __name__ == "__main__":
    main()
