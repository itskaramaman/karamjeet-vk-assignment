import React, { useState, useEffect } from "react";
import { newsCategories } from "../../utils";

const Home = () => {
  const [newsData, setNewsData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [category, setCategory] = useState("");

  useEffect(() => {
    // Function to fetch data from the backend
    const fetchData = async () => {
      setLoading(true);
      try {
        const url =
          category == ""
            ? `http://127.0.0.1:5000/data`
            : `http://127.0.0.1:5000/data/${category}`;
        const response = await fetch(url);
        const data = await response.json();
        console.log(data);
        setNewsData(data);
      } catch (error) {
        console.error("Error fetching news data:", error);
      }
      setLoading(false);
    };

    fetchData();
  }, [category]);

  return (
    <div className="max-w-screen-lg mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-6">BBC News Scraper</h1>
      <select
        id="category"
        value={category}
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
        {newsData.map((item, index) => (
          <div
            key={index}
            className="bg-white shadow-lg rounded-lg p-4 hover:shadow-xl transition"
          >
            {item.image_url && (
              <img
                src={item.image_url}
                alt={item.headline}
                className="w-full h-48 object-cover rounded-md mb-4"
              />
            )}
            <h3 className="text-xl font-semibold text-gray-800 mb-2">
              {item.headline}
            </h3>
            <p className="text-gray-600 text-sm mb-4">{item.description}</p>
            {item.news_link && (
              <a
                href={item.news_link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-500 hover:text-blue-700 text-sm"
              >
                Read more
              </a>
            )}
            <div className="text-xs text-gray-500 mt-2">
              <p>{item.last_updated}</p>
              {item.tag && <p className="italic">{item.tag}</p>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
