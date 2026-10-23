# アーキテクチャ

- 状態：初期案（ONE-1で検証・調整）
- 参照：Confluence「02_基本設計」v0.2

## 構成

```text
PC / スマホブラウザ
      |
      v
Django (Templates + HTMX)
      |
      v
PostgreSQL
```

単一Djangoアプリケーションとして構成する。業務ロジックと永続化はDjango側で扱い、必要な部分更新にHTMXを使う。

## 開発環境

Docker ComposeでWeb（Python/Django）とDB（PostgreSQL）の2サービスを起動する。DBはホスト側ポートを公開しない。Djangoの8000番はローカルループバックのみに公開する。

初期Djangoアプリ `core` は起動確認用の画面を提供するだけで、勤怠機能を含まない。認証・勤務条件・勤怠管理などのアプリ分割は関連チケットの設計段階で決める。

## 本番運用の予定（未実装）

AWSを利用する方針だが、アーキテクチャは未決定。Nginx・Gunicorn・HTTPS・DB閉域化・バックアップ・監視・秘密情報の管理が必要。開発用の `runserver` を本番公開に流用しない。

## 開発時の依存関係

- `ONE-1` 開発環境構築 → `ONE-2` ユーザー認証などの業務機能へ。
- Excel出力は会社指定Excelテンプレートの詳細確定待ち。
