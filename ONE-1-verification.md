# ONE-1 受入チェック（開発環境構築）

- Jira: [ONE-1](https://one-2ka-devlab.atlassian.net/browse/ONE-1)
- 目的: メンバー全員が同じ手順でDjango + PostgreSQLの環境を再現できること
- 状態: **手元で実行してから承認するチェックリスト**（未実施の項目にはチェックを付けない）

## 事前準備

- Docker Desktop（またはDocker Engine + Compose）を起動する
- `cp .env.example .env` を実行する
- `.env` 内で `DJANGO_SECRET_KEY` と `POSTGRES_PASSWORD` を独自の値に変更する
- `.env` をGitへコミットしない（`git status --ignored` で確認可能）

## 作業確認

```bash
docker compose config --quiet
docker compose up --build -d
docker compose ps
docker compose exec web python manage.py check
docker compose exec web python manage.py migrate
docker compose exec web python manage.py test
docker compose exec web python manage.py makemigrations --check --dry-run
```

## 受入条件と確認証跡

- [ ] `docker compose config --quiet` が成功
- [ ] `docker compose ps` でWebとDBが起動（DBはhealthy）
- [ ] `docker compose exec web python manage.py migrate` が成功（DB接続成功）
- [ ] `docker compose exec web python manage.py test` が成功（DB `SELECT 1` テストを含む）
- [ ] `http://localhost:8000/` でDeep Tealの初期画面が表示される
- [ ] 2人目のメンバーがREADMEだけを見て同じ結果を再現できる
- [ ] GitHub ActionsのCIが成功
- [ ] `.env` や実際の勤怠情報が公開リポジトリに含まれない
- [ ] Pull Requestにレビューがあり、承認後にマージしている

## よくあるトラブル

- `DJANGO_SECRET_KEY` エラー: `.env` に生成した秘密鍵を設定したか確認
- DBに接続できない: `docker compose ps` と `docker compose logs db` を確認
- `localhost:8000` に表示されない: 他のアプリによるポート競合と `docker compose logs web` を確認
- パッケージを変更した場合: `docker compose up --build -d` で再ビルド
- DBボリュームを削除する `docker compose down -v` はデータを失うので慎重に扱う

本チケットで勤怠業務モデル・ログイン画面は実装しない。続きはONE-2以降で設計・受入条件を確認してから実装する。
