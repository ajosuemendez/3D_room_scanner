
const express = require("express");
const router = express.Router();
const { displayModel, getModels, sortModels } = require('../controllers/modelController');

  
router.get("/", getModels);
//router.get("/models", getModels);
router.post("/", sortModels);
//router.post("/models", sortModels);
router.get("/models/:id", displayModel);

module.exports = router;