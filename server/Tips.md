- send
  - event 名が message 固定
- emit
  - event 名を指定できる
  
- db.Modelの__dict__をオーバーライドすると謎のエラーが出るので注意

- sqlalchemy の relationship はデフォルトで lazy load だが，
    - Query に options で selectload を使い指定すれば eager laod になる
    
## cascade
all == save-update, merge, refresh-expire, expunge, delete,
- save-update
    - session の中で，親に子供に関する変更がされたときや追加されたときに，
    - 子供も save update される 
- delete
    - 親が消えたとき子供も消える
- delete-orphan
    - 親は残っているが親の方から子供への参照を外したとき，
    - 子供は消える