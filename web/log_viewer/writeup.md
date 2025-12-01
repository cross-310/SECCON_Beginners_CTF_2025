# Writeup
問題の実装は下記の通り (抜粋)

```golang
package main

var tpl = template.Must(
...

func init() {
	...

	flag.StringVar(&flagValue, "flag", "ctf4b{this_is_dummy_flag}", "flag")
	flag.Parse()
	...

}
...

var handlerFunc http.HandlerFunc = func(w http.ResponseWriter, r *http.Request) {
	file := r.URL.Query().Get("file")
	slog.Info("handlerFunc", slog.String("file", file))
	...

	content["Path"] = "logs/" + file
	b, err := os.ReadFile(content["Path"])
	...

	content["Content"] = html.EscapeString(string(b))
	tpl.Execute(w, content)
}
```

今回のアプリケーションは、ディレクトリ・トラバーサルの脆弱性があり任意のファイルが表示できるようになっている. また Linux には、アプリケーションの起動時に付与したコマンドライン引数は `/proc/<PID>/cmdline` にアクセスすることで表示できる機能がある. (※ コマンド自身の情報は、 PID を直接指定する代わりに `self` をエイリアスとして利用できる.)  

そのため `?file=../../proc/self/cmdline` のクエリを付与してアクセスするとフラグが入手できる  
