import React, { useState, useEffect } from "react";
import { newsCategories, sportsCategory } from "../../utils";
import NewsCard from "../components/NewsCard";

const Home = () => {
  const [newsData, setNewsData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [category, setCategory] = useState("");
  const [subCategory, setSubCategory] = useState("");
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);

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
        let url;

        if (category === "") {
          url = `http://127.0.0.1:5000/data?page=${page}`;
        } else if (category === "sports" && subCategory !== "") {
          url = `http://127.0.0.1:5000/data/${category}/${subCategory}?page=${page}`;
        } else {
          url = `http://127.0.0.1:5000/data/${category}?page=${page}`;
        }

        const response = await fetch(url);
        const data = await response.json();
        setNewsData(data.news);
        setHasNext(data.has_next);
      } catch (error) {
        console.error("Error fetching news data:", error);
      }
      setLoading(false);
    };

    fetchNews();
  }, [category, page, subCategory]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-4xl">BBC News</h1>
      <div className="flex items-center gap-5">
        <select
          id="category"
          value={category}
          className="border-2 border-gray-200 rounded-md mt-4"
          onChange={(e) => {
            setCategory(e.target.value);
            setPage(1);
          }}
        >
          {newsCategories.map((category, index) => (
            <option key={index} value={category}>
              {category.toUpperCase() || "All"}
            </option>
          ))}
        </select>

        {category === "sports" && (
          <select
            id="category"
            value={subCategory}
            className="border-2 border-gray-200 rounded-md mt-4"
            onChange={(e) => setSubCategory(e.target.value)}
          >
            {sportsCategory.map((category, index) => (
              <option key={index} value={category}>
                {category.toUpperCase() || "All"}
              </option>
            ))}
          </select>
        )}
      </div>

      {loading && <div className="mt-4 text-center text-xl">Loading...</div>}

      <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {newsData.map((news) => (
          <NewsCard news={news} key={news.id} handleDelete={handleDelete} />
        ))}
      </div>

      <div className="flex justify-center my-10 gap-2">
        <button
          disabled={page == 1}
          onClick={() => setPage((prev) => prev - 1)}
          className={`bg-blue-400 text-white p-1 cursor-pointer hover:bg-blue-500 rounded-md`}
        >
          Prev
        </button>
        <label className="bg-gray-100 py-1 px-3">{page}</label>
        <button
          disabled={!hasNext}
          onClick={() => setPage((prev) => (hasNext ? prev + 1 : prev))}
          className="bg-blue-400 text-white p-1 cursor-pointer hover:bg-blue-500 rounded-md"
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default Home;
