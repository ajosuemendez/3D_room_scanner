
const data = [
  { "id": "1",
    "name": "model1.ply",
    "size": "100000MB",
    "date": "22.34.2023"},
  { "id": "2",
    "name": "model2.ply",
    "size": "4300MB",
    "date": "21.50.2027"},

  { "id": "3",
    "name": "model3.ply",
    "size": "567000MB",
    "date": "22.20.2023"}
];

const fileFunc = require("../../public/javascript/directoryFunctions")

function getModel(id){
    for(let i=0; i<data.length; i++){
        if (data[i].name === id) {
          return data[i];
        }
      }
      return undefined
}

function displayModel(req, res){
  const id = req.params.id;
  //const model = getModel(id);

  return res.render("modelLayout", {modelName: id})
  //if (model === undefined) {
  //  return res.render("modelLayout", {modelName: id})
  //}
  //return res.render("modelLayout", {modelName: model.name});

}

async function getModels(req, res, next) {
    var data = await fileFunc.getAllFilesInDirectory();
    var sortButtons = ["date", "size", "name"]
    console.log(data)
    res.render('index', { myTitle: 'Camera-Scanner' , sortButtons : sortButtons, data : data});
    //res.render("index", { title: "Home"});
}

async function sortModels(req, res) {
    console.log(req);
    var sortButtons = ["date", "size", "name"]
    var sortType = req.body.sortType;
    console.log(sortType);
    var data = await fileFunc.getAllFilesInDirectory();
    var names = [];
    if(sortType === 'name'){
      data.sort(function(a,b){
        return a.name.localeCompare(b.name)
      })
    } else if (sortType === 'date'){
      data.sort(function (a,b){
        return new Date(a.birthtime) - new Date(b.birthtime)
      })
    } else if (sortType === 'size'){
      data.sort(function(a,b){
        return a.size - b.size
      })
    }

    data.forEach(function (file) {
      names.push(file.birthtime)
    });

    console.log("storted data:", data);

    res.render('index', { myTitle: 'Camera-Scanner', sortButtons : sortButtons, data : data});
}

module.exports = { displayModel, getModels, sortModels}