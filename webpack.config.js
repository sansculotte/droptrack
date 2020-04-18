const path = require('path')

module.exports = (env, args) => {
  return { 
    entry: {
      main: './webapp-js/main.jsx'
    },
    output: {
      filename: '[name].bundle.js',
      chunkFilename: '[name].bundle.js',
      path: __dirname + '/webapp/static/scripts',
      publicPath: '/scripts/'
    },
    devtool: 'source-map',
    resolve: {
      extensions: ['.js', '.jsx', '.json', '.ts', '.tsx'],
      modules: [path.resolve(__dirname, 'webapp-js'), 'node_modules'],
      alias: {
        deepmerge$: path.resolve(
            __dirname,
            'node_modules/deepmerge/dist/umd.js'
        )
      }
    },
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader"
          }
        },
        {
          test: /\.(ts|tsx)$/,
          exclude: /node_modules/,
          use: ["babel-loader", "ts-loader"]
        },
        {
          test: /\.css$/,
          use: ['style-loader', 'css-loader']
        },
        {
          test: /\.scss$/,
          include: path.join(__dirname, 'webapp-js'),
          use: [
            'style-loader',
            {
              loader: 'typings-for-css-modules-loader',
              options: {
                modules: true,
                 localIdentName: '[path][name]__[local]',
                 namedExport: true,
                 importLoaders: 2,
                 exportOnlyLocals: true
              }
            },
            'sass-loader'
          ]
        }
      ]
    }
  }
}
