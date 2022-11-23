const fs = require('fs');
const child_process = require('child_process')
const unzipper = require('unzipper')
const axios = require('axios')

function getPlatform() {
    var platform = process.platform;

    if (platform == 'darwin') {
        return 'osx';
    }
    if (platform == 'win32') {
        return 'windows';
    }
    if (platform == 'linux') {
        return 'linux';
    }

    console.error(`platform ${platform} not supported... exiting`)
    process.exit()
}

async function downloadBinaryFromGithub(platform) {
    var downloadUrl = `https://github.com/diggerhq/dgctl/releases/download/latest-release/dgctl-${platform}.zip`;
    var zipFile = "dgctl.zip";

    console.log(`Fetching ${downloadUrl}`)

    await axios.get(downloadUrl, {
      responseType: 'stream',
    }).then((response) => {
      response.data.pipe(fs.createWriteStream(zipFile))
        .on('close', function() {
          fs.createReadStream(zipFile).pipe(unzipper.Extract({path: "."}))
            .on('close', function() {
              fs.unlinkSync(zipFile);
              if (platform == "osx") {
                child_process.execSync(`chmod +x dgctl`)
                console.log("Well done! You can run './dgctl' now");
              }

              if (platform == "windows") {
                console.log("Well done! You can run 'dgctl.exe' now");
              }
            });
          });
    });

}

async function installFromPip() {
    console.log(`Installing dgctl from Python Package Repository`)
    child_process.execSync(`python -m pip install dgctl`)
}

async function main() {
    var homedir = require('os').homedir()
    var platform = getPlatform()

    if (platform == "linux") {
        await installFromPip();
        console.log("Well done! You can run 'dgctl' now");
        return;
    }

    await downloadBinaryFromGithub(platform);
}

main()
