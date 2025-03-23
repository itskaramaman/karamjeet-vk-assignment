import React from "react";

const NewsCard = ({ news, handleDelete }) => {
  return (
    <div className="bg-white shadow-lg rounded-lg p-4 hover:shadow-xl transition relative">
      {news.image_url && (
        <img
          src={news.image_url}
          alt={news.headline}
          className="w-full h-48 object-cover rounded-md mb-4"
        />
      )}
      <h3 className="text-xl font-semibold text-gray-800 mb-2">
        {news.headline}
      </h3>

      <p className="text-gray-600 text-sm mb-4 line-clamp-3">
        {news?.description}
      </p>
      {news.news_link && (
        <a
          href={news.news_link}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-500 hover:text-blue-700 text-sm"
        >
          Read more
        </a>
      )}
      <div className="flex justify-between text-xs text-gray-500 mt-2">
        <p>{news.last_updated}</p>
        {news.tag && <p className="italic">{news.tag}</p>}
      </div>

      <button
        onClick={() => handleDelete(news.id)}
        className="absolute cursor-pointer top-2 right-2 bg-red-500 text-white text-xs px-2 py-1 rounded hover:bg-red-600 transition"
      >
        Delete
      </button>
    </div>
  );
};

export default NewsCard;
