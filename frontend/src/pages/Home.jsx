import React, { useState, useEffect } from "react";
import { newsCategories } from "../../utils";
import NewsCard from "../components/NewsCard";

const Home = () => {
  const [newsData, setNewsData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [category, setCategory] = useState("");

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/delete/${id}`, {
        method: "DELETE",
      });

      if (response.ok) {
        setNewsData(newsData.filter((news) => news.id != id));
      } else {
        console.error("Failed to delete news");
      }
    } catch (error) {
      console.error("Error deleting news:", error);
    }
  };

  useEffect(() => {
    const fetchNews = async () => {
      setLoading(true);
      try {
        const url =
          category == ""
            ? `http://127.0.0.1:5000/data`
            : `http://127.0.0.1:5000/data/${category}`;
        const response = await fetch(url);
        const data = await response.json();
        setNewsData(data);
      } catch (error) {
        console.error("Error fetching news data:", error);
      }
      setLoading(false);
    };

    fetchNews();
  }, [category]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl">BBC News</h1>
      <select
        id="category"
        value={category}
        className="border-2 border-gray-200 rounded-md mt-4"
        onChange={(e) => setCategory(e.target.value)}
      >
        {newsCategories.map((category, index) => (
          <option key={index} value={category}>
            {category.toUpperCase() || "All"}
          </option>
        ))}
      </select>

      {loading && <div className="mt-4 text-center text-xl">Loading...</div>}

      <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {newsData.map((news, index) => (
          <NewsCard news={news} index={index} handleDelete={handleDelete} />
        ))}
      </div>
    </div>
  );
};

export default Home;
