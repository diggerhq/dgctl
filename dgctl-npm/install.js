const download = require('download-file')
const fs = require('fs');
const child_process = require('child_process')
const unzipper = require('unzipper')
const axios = require('axios')

function getPlatform() {
    var platform = process.platform;

    if (platform == 'darwin') {
        return 'osx';
    } else if (platform == 'win32') {
        return 'windows'
    } else { 
        console.error(`platform ${platform} not supported .. exiting`)
        process.exit()
    }
}

async function main() {
    var homedir = require('os').homedir()
    var platform = getPlatform()
    var downloadUrl = `https://github.com/diggerhq/dgctl/releases/download/latest-release/dgctl-${platform}.zip`;

    console.log(`Fetching ${downloadUrl}`)

    await axios.get(downloadUrl, {
      responseType: 'stream',
    }).then((response) => {
      response.data.pipe(fs.createWriteStream("dgctl.zip"))
        .on('close', function() {
          fs.createReadStream("dgctl.zip").pipe(unzipper.Extract({path: "."}))
            .on('close', function() {
              if (platform == "osx") {
                child_process.execSync(`chmod +x dgctl`)
                console.log("Well done! Run ./dgctl");
              }

              if (platform == "windows") {
                console.log("Well done! Run dgctl.exe");
              }
            });
          });
    });
}

main()
