# ONE-2 検証チェックリスト（ログイン・ログアウト）

- Jira: https://one-2ka-devlab.atlassian.net/browse/ONE-2
- Figma PC: https://www.figma.com/design/lSCe6VjaA5dKl8qCnMGFlZ?node-id=4-224
- Figma スマホ: https://www.figma.com/design/lSCe6VjaA5dKl8qCnMGFlZ?node-id=5-84
- 関連仕様: [Requirements.md](Requirements.md) F-01 / [Spec.md](Spec.md) §2
- 状態：**コード追加済み・実行検証とチームレビュー待ち**

## 開発環境

前提：ONE-1の `docker compose up --build -d` とDBマイグレーションが完了していること。

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py check
docker compose exec web python manage.py test
```

手動テスト用ユーザー（開発専用）の作成例：

```bash
docker compose exec web python manage.py createsuperuser
```

※実社員のアカウントやパスワードを使わず、ダミーの値で作成してください。

## 手動確認

- [ ] 未認証で `http://localhost:8000/` にアクセスすると `/login/?next=/` に転送される
- [ ] PC幅でネイビー×白のログイン画面を表示できる
- [ ] スマホ幅で縦長のログイン画面を表示できる（Figma v0.2）
- [ ] 正しいユーザー名/パスワードでログインし `/` が表示される
- [ ] 誤ったユーザー名/パスワードでエラーが表示され、ログインできない
- [ ] ダッシュボードにログインユーザー名が表示され、勤怠データは未表示
- [ ] ログアウトボタンでセッション終了し `/login/` に戻る
- [ ] ログアウト後に `/` へアクセスすると再ログインを求められる
- [ ] `GET /logout/` がログアウトせず 405 となる
- [ ] CSRFトークンがないPOSTは403になる
- [ ] `next=https://external.example/` で外部サイトへリダイレクトしない
- [ ] 別ユーザーの勤怠データ閲覧については、データモデルと勤怠画面実装後のチケットで検証する

## 既知の未実装

- 自己登録、メールアドレスログイン、パスワード再設定
- 勤怠データモデルおよび本人データへのアクセス制御（ONE-8〜14に依存）
- ログイン画面の本番公開・HTTPS終端は別設計

## 完了判定

自動テスト、実機確認、人間レビュー、PRマージ後にJiraの受入条件を確認してから完了にする。
