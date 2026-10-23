# 実装仕様書インデックス

**ここに置く仕様が開発時の正本です。** 現在の資料はConfluenceの「01_要件定義」「02_基本設計」（いずれも v0.2・Draft）を参考に移行した**初期案**で、チームでレビューした後に正式確定します。

| 文書 | 役割 |
| --- | --- |
| [Requirements.md](Requirements.md) | 背景、対象範囲、機能要件、ビジネスルール |
| [Spec.md](Spec.md) | 具体動作、受入条件、未決事項 |
| [architecture.md](architecture.md) | システム構成、開発・本番環境方針 |
| [database.md](database.md) | データモデル候補と設計上の未決事項 |
| [development-rules.md](development-rules.md) | チケット運用、PR、AI開発、完了条件 |
| [ONE-1-verification.md](ONE-1-verification.md) | ONE-1の環境構築・受入確認チェックリスト |
| [ONE-2-verification.md](ONE-2-verification.md) | ONE-2の認証・画面・安全性チェックリスト |

関連情報：
- [Claude Codeへの共通指示](../CLAUDE.md)
- [Jira ONE](https://one-2ka-devlab.atlassian.net/jira/software/projects/ONE/boards/2/backlog)
- Confluence： [要件定義](https://one-2ka-devlab.atlassian.net/wiki/spaces/2D/pages/65729)、[基本設計](https://one-2ka-devlab.atlassian.net/wiki/spaces/2D/pages/327698)

## 仕様書の更新

- 必要に応じて仕様を改善。タイミングは担当者の判断でよいが、仕様変更は人間の承認を得る。
- 変更がコードや受入条件に影響する場合、関連テストも更新して同じPRでレビューする。
- 文書が長くなった場合や並行編集が増えた場合は、機能単位でサブディレクトリへ分割する（約300行は目安、必須ではない）。
- 仕様本文を複数箇所へ複製しない。概要とリンクを活用する。
