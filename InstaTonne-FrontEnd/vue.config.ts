publicPath: 'http://localhost:8080' //base url where app gets deployed!
outputDir: '../static/dist' //path for static files when built
indexPath: '../templates/_base_vue.html' //path for generated index file that django will use


configureWebPack: {
    devServer: {
        devMiddleware: {
            writeToDisk: true
        }
    }
}

