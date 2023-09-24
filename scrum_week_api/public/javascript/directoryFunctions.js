var fs = require('fs');
const path = require('path');
const directoryPath = "/home/scrumpractice/scrum_week_api/public/models/ply/";


//createNewFile("newDoumentName")
//deleteFile("newDoumentName")
//renameFile("testtxt2", "testtxt3")
//getAllFilesInDirectory()
//moveFile(directoryPath, path.join(__dirname, 'newFolder'))
//console.log(getSizeOfFile("testtxt.txt"))
//console.log(inputArray.sort(sortListByProperty("value")))


function getSizeOfFile(file){
  var stats = fs.statSync(path.join(directoryPath, file))
  var fileSizeInBytes = stats.size;
  var fileSizeInKilobytes = fileSizeInBytes / (1024);
  fileSizeInKilobytes = fileSizeInKilobytes + ""
  var digitsAfterComma = fileSizeInKilobytes.substr(fileSizeInKilobytes.indexOf(".") + 1, fileSizeInKilobytes.size)
  if(digitsAfterComma > 1000){
    fileSizeInKilobytes = fileSizeInKilobytes.substr(0 , fileSizeInKilobytes.indexOf(".") + 4)
  }
  return fileSizeInKilobytes
}

function getBirthtimeOfFile(file){
  var stats = fs.statSync(path.join(directoryPath, file))
  var timeStamp = stats.birthtime
  return timeStamp
}

function sortListByProperty(property) {
  var sortOrder = 1;
  if(property[0] === "-") {
      sortOrder = -1;
      property = property.substr(1);
  }
  return function (a,b) {
      /* next line works with strings and numbers, 
       * and you may want to customize it to your needs
       */
      var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
      return result * sortOrder;
  }
}

function moveFile(oldPath, newPath){
  fs.rename(oldPath, newPath, function (err) {
    if (err) throw err
    console.log('Successfully renamed - AKA moved!')
  })
}

async function getAllFilesInDirectory(){
  var counter = 0;
  
  var promise = new Promise((resolve, reject) => {
    var hdata = []
    fs.readdir(directoryPath, function (err, files) {
      //handling error
      if (err) {
          console.log('Unable to scan directory: ' + err);
          reject(err)
          return
      } 
      //listing all files using forEach
      files.forEach(function (file) {
        var newObject = {}
        newObject.name = file;
        newObject.size = getSizeOfFile(file);
        newObject.birthtime = getBirthtimeOfFile(file);
        hdata.push(newObject);
      });

      resolve(hdata)
      //hier funktionierts
    });  
  })
  var data = await promise
  

  //console.log(data)
  return data
}
console.log(getAllFilesInDirectory())

module.exports = {
  getAllFilesInDirectory : getAllFilesInDirectory,
  sortListByProperty : sortListByProperty
}