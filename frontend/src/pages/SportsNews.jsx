import { useState, useEffect } from "react";
import Loader from "../components/Loader";
import NewsCard from "../components/NewsCard";
import { sportsCategory } from "../../utils";

const SportsNews = () => {
  const [category, setCategory] = useState("");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);

  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/delete/${id}`, {
        method: "DELETE",
      });

      if (response.ok) {
        setData(data.filter((news) => news.id != id));
      } else {
        console.error("Failed to delete news");
      }
    } catch (error) {
      console.error("Error deleting news:", error);
    }
  };

  useEffect(() => {
    const fetchSportsNews = async () => {
      try {
        setLoading(true);
        const url =
          category == ""
            ? "http://127.0.0.1:5000/sports-data"
            : `http://127.0.0.1:5000/sports-data/${category}`;

        const response = await fetch(url);
        const data = await response.json();
        setData(data);
      } catch (error) {
        console.error("Error fetching sports news:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSportsNews();
  }, [category]);

  return (
    <div className="min-h-screen w-full">
      <div className="container mx-auto py-5">
        <h1 className="text-4xl">BBC Sports News</h1>
        <select
          id="category"
          value={category}
          className="border-2 border-gray-200 rounded-md mt-5"
          onChange={(e) => setCategory(e.target.value)}
        >
          {sportsCategory.map((category, index) => (
            <option key={index} value={category}>
              {category.toUpperCase() || "All"}
            </option>
          ))}
        </select>
        <div>
          {loading ? (
            <Loader />
          ) : (
            <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
              {data.map((news) => (
                <NewsCard
                  key={news.id}
                  news={news}
                  handleDelete={handleDelete}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SportsNews;
