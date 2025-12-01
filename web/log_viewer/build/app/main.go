package main

import (
	"flag"
	"fmt"
	"html"
	"log/slog"
	"net/http"
	"os"
	"text/template"
)

var (
	flagValue string // This is the flag
	portNum   int    // Port number
)

var tpl = template.Must(template.New("index").Parse(`
<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>LogViewer</title>
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/uikit@3.23.7/dist/css/uikit.min.css" />
</head>
<body>
	<div class="uk-container uk-margin-top">
		<h1>Internal LogViewer</h1>
		<h2>🔍 Select a file </h2>
		<form method="GET" action="/" class="uk-margin uk-form">
			<select name="file" id="file" class="uk-select uk-form-width-large">
				<option value="">Select a file</option>
				<option value="access.log">access.log</option>
				<option value="debug.log">debug.log</option>
			</select>
			<button type="submit" class="uk-button uk-button-default">View</button>
		</form>

		{{if .Path}}
		<h2>📄 File: {{.Path}}</h2>
		<pre class="uk-margin-small uk-card uk-card-default uk-card-body uk-background-muted"><code>{{.Content}}</code></pre>
		{{end}}
	</div>
</body>

</html>
`))

func init() {
	slog.Info("Initializing LogViewer...", slog.Int("pid", os.Getpid()))

	flag.StringVar(&flagValue, "flag", "ctf4b{this_is_dummy_flag}", "flag")
	flag.IntVar(&portNum, "port", 8000, "port")
	flag.Parse()

	slog.Debug("Parsed command line arguments", slog.String("flag", flagValue), slog.Int("port", portNum))
}

func main() {
	http.HandleFunc("/", handlerFunc)
	http.ListenAndServe(fmt.Sprintf(":%d", portNum), nil)
}

var handlerFunc http.HandlerFunc = func(w http.ResponseWriter, r *http.Request) {
	file := r.URL.Query().Get("file")
	slog.Info("handlerFunc", slog.String("file", file))

	if len(file) < 1 {
		tpl.Execute(w, nil)
		return
	}

	content := make(map[string]string)
	content["Path"] = "logs/" + file

	b, err := os.ReadFile(content["Path"])
	if err != nil {
		content["Content"] = "File not available"
		slog.Error("File not available", slog.String("file", content["Path"]), slog.Any("err", err))
		w.WriteHeader(http.StatusNotFound)
		tpl.Execute(w, content)
		return
	}

	content["Content"] = html.EscapeString(string(b))
	tpl.Execute(w, content)
}
