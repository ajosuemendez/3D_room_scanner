const express = require('express');
const app = express();
const path = require("path");
const cookieParser = require('cookie-parser')


app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({extended: false}));
const models = require("./routes/models.js");
app.use("/", models);

app.set("views", path.join(__dirname, "views"));
app.set("view engine", "pug");

app.use(cookieParser());



const PORT = process.env.PORT || 5000;

const server = app.listen(PORT, () => {
  console.log("server is running on port", server.address().port);
});