const express = require("express");
const { exec } = require("child_process");
const cors = require("cors");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(cors());
app.use(express.json());

app.post("/api/v1/search", (req, res) => {
  
  let { searchTerm } = req.body;
  // searchTerm = "ayurvedic " + searchTerm
  console.log(req.body);

  exec(
    `python3 /Users/samarjeetsingh/Desktop/suggestion/webscraoer.py "${searchTerm}"`,
    (error, stdout, stderr) => {
      if (error) {
        return res.status(500).json({ message: "Scraper error", error });
      }
      try {
        const filePath = path.join(__dirname, "amazon_products.json");
        const result = fs.readFileSync(filePath, {
          encoding: "utf8",
          flag: "r",
        });

        // Ensure it's a valid JSON response
        res.json(JSON.parse(result));
      } catch (e) {
        res
          .status(500)
          .json({ error: "Invalid JSON response", details: e.message });
      }
    }
  );
});

app.listen(8000, () => console.log("Server running on port 8000"));
