module.exports = {
    apps: [
      {
        name: 'WallyDevNuxt',
        cwd: '<폴더경로>/wallydev',
        exec_mode: 'cluster',
        instances: '1', // Or a number of instances
        script: './node_modules/nuxt/bin/nuxt.js',
        args: 'start',
        autorestart: true,
        env: {
            HOST: '0.0.0.0',
            PORT: 82,
            NODE_ENV: 'production'
        },
        output: './logs/console.log',
        error: './logs/consoleError.log'
      }
    ]
  }
