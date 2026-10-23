# One勤怠管理システム

2課 DevLab による **AI駆動開発の学習プロジェクト**。日々の勤怠を記録し、勤務時間・残業時間を可視化し、将来的に会社所定のExcel形式へ出力するWebアプリケーションです。

> **現在の状態：ONE-1 + ONE-2の実装案**。Django・PostgreSQL・Dockerの開発基盤に、ログイン／ログアウト／認証済み画面のアクセス制御を追加しました。**打刻、勤怠データモデル、残業計算、Excel出力は未実装**です。PRと人間レビューが済むまで、各チケットは完了扱いにしません。

## 技術スタック

- Python 3.12 / Django 5.2 LTS
- PostgreSQL 16
- Docker / Docker Compose
- Django Templates + HTMX（HTMXは機能実装時に導入）
- GitHub / Jira / Claude Code

## 1. 起動方法

Docker Desktop または Docker Engine + Docker Compose が必要です。

```bash
cp .env.example .env
```

`.env` 内の `DJANGO_SECRET_KEY` および `POSTGRES_PASSWORD` を**自分用の値**に変更してください。シークレットキー生成例：

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

```bash
docker compose up --build -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py check
docker compose exec web python manage.py test
```

http://localhost:8000/ で **Deep Tealの開発用初期画面**を確認します。

上記の `migrate` は実際のPostgreSQL接続を確認し、`test` は `SELECT 1` でDB疎通も検証します。`check` は構成チェックです。ブラウザ表示だけではDB接続確認にならないため、必ず3つとも実行してください。

```bash
docker compose logs -f web       # ログを見る
docker compose down              # 停止（DBデータは保持）
docker compose down -v           # DBボリュームも削除（要注意）
```

## 2. 開発用コマンド

```bash
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate
docker compose exec web python manage.py test
docker compose exec web python manage.py createsuperuser
```

※管理画面・`createsuperuser` は開発者向けです。ONE-2のログイン・ログアウトは実装されていますが、一般ユーザーの作成・配布方法、メールアドレスログイン、パスワード再設定は仕様未確定・未実装です。

## 3. ドキュメント

- [docs/README.md](docs/README.md) — 仕様書の入口
- [docs/Requirements.md](docs/Requirements.md) — 要求・機能範囲
- [docs/Spec.md](docs/Spec.md) — システムの振る舞い・受入条件
- [docs/architecture.md](docs/architecture.md) — 技術構成
- [docs/database.md](docs/database.md) — データ方針と未決事項
- [docs/development-rules.md](docs/development-rules.md) — Jira・GitHub・AI開発ルール
- [CLAUDE.md](CLAUDE.md) — Claude Code共通指示
- [docs/ONE-2-verification.md](docs/ONE-2-verification.md) — ONE-2認証の検証チェックリスト

Jiraプロジェクト：[ONE](https://one-2ka-devlab.atlassian.net/jira/software/projects/ONE/boards/2/backlog)  
UIデザイン：[One Attendance — Figma (Deep Teal)](https://www.figma.com/design/lSCe6VjaA5dKl8qCnMGFlZ)

## 4. 継続的インテグレーション（CI）

GitHub Actions (`.github/workflows/ci.yml`) は `main` へのpushとPRで、PostgreSQL 16サービスを起動してから `check`・`migrate`・マイグレーション差分検出・`test` を実行します。

Python/Djangoがインストールされていないこの文書作成環境やDocker未導入環境ではテストできません。CIが緑になったことと、メンバーのDocker環境で起動できたことをもって受入確認を行います。

## 5. 運用・セキュリティ

- `docs/` は実装仕様の正本です。Confluenceは企画・協議・議事録、Jiraはタスク・スプリント管理に使います。
- 原則 `feature/ONE-xxx-description` ブランチで実装し、PRで人間レビューを受けてから `main` にマージします。初回の雛形だけは直接 `main` に配置できます。
- `.env`、APIキー、パスワード、個人の勤怠データ、社内の非公開資料はコミットしないでください。公開リポジトリです。
- `docker compose` のDjango開発サーバーは**ローカル開発専用**です。実データを扱うインターネット公開用途には使わないでください。
- 本番公開に必要なHTTPS、認可、DB閉域化、ログ、バックアップ等は未整備です。

## 6. 初回タスクとの関係

- `ONE-1` 開発環境構築：この雛形を各メンバー環境で再現・確認して完了判定します。**雛形の作成・静的検証だけではチケット完了とはしません。**
- `ONE-2` ユーザー認証：ログイン・ログアウトと認証済み画面へのアクセス制御を実装しました。自動テストとレビューが完了するまで **検証中** としてください。
