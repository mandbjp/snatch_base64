# snatch_base64

## 目次

- 名前付きPIPE
- script コマンド
- `snatch_base64.py` 機能
- 以上ですが、嘘かもしれない

---

## Qiita

https://qiita.com/mandbjp505/items/77ea497e12ca23e221ac

---


## 名前付きPIPE
---

## 名前付きPIPEって？

- 通常のPIPEは `|` で stdout -> stdin をつなぐ
- 名前付きPIPEは `mkfifo` で作られたファイル越しに stdout -> stdin をつなぐ


---

## 名前付きPIPE 使い方

```shell:term1
> mkfifo -m 0777 my_fifo.pipe
> cat my_fifo.p
(ここで止まる)
```

```shell:term2
> echo "hello!" > my_fifo.pipe
> 
```

```shell:term1
> mkfifo -m 0777 my_fifo.pipe
> cat my_fifo.p
hello!
> 
```

---

## 名前付きPIPE 特徴

- ターミナルが別でも伝搬可能
- 実行ユーザーが別でも伝搬可能 `(-m 0777)　オプション`
- 入出力が揃わないと開始しない
- 名前付きPIPEへの出力 (`term2`) が終了すると、 名前付きPIPEからの入力 (`term1`) も終了する

---

## script コマンド
---

## script コマンド (Mac/FreeBSD系)

- stdin/stdout を記録してくれる
- `-F` : 名前付きPIPEへ出力する
- `-q` : 開始/終了メッセージを表示しない

---

## script使い方 (ターミナルをミラー化)

```shell:term1
> mkfifo -m 0777 my_fifo.pipe
> cat my_fifo.pipe
（待つ）
```

```shell:term2
> script -qF my_fifo.pipe
> （ここで何かを入力する）
```

```shell:term1
> mkfifo -m 0777 my_fifo.pipe
> cat my_fifo.pipe
(全く同じ挙動がここで見える)
```

- ターミナルをリサイズして `vim` とかやると面白い

---

## script 特徴

-  stdin/stdout 両方取れる
-  ただし、stdin/stdout の区別はできない

---

## `snatch_base64.py` の機能
---

## `snatch_base64.py` がやってること

1. 名前付きPIPEをFileOpenする
-  → ユーザーの入力も、コマンドの結果も読み取れる
- 改行区切りで入力を判定する
- `(centos用) base64 -w0` の文字列が含まれるか
- `(mac用) base64 -i -` の文字列が含まれるか
- 含まれている場合、次の行をbase64入力として準備する
- 改行を見つけるまでメモリ上に貯め込む
- 改行されたら溜め込んだものを base64decode してファイル保存する

---

## `snatch_base64.py` の強み

- ローカルのstdin/stoutしか見ないため、多段のsshにも対応
- 先方サーバーにはツール等のインストールが不要
    - base64コマンドが必要
- `gzip` 検出で保存時にgz展開
- `cat` 検出でファイル名取得

---

## 以上ですが、嘘かもしれない

- 本書の内容は経験的なことで書いてます
- 正しくない情報が含まれてるかもしれません
- 間違ってたらごめんなさい

---

## _End of Slide_
