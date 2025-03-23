import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="shadow-sm py-5 px-10 flex justify-between items-center">
      <h2 className="text-2xl bg-gradient-to-r from-pink-500 via-purple-500 to-blue-500 text-transparent bg-clip-text">
        BBC News Scrapper
      </h2>
      <ul className="flex gap-5 items-center">
        <li>
          <Link
            className="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-md"
            to="/"
          >
            News
          </Link>
        </li>
        <li>
          <Link
            className="bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-md"
            to="/sports"
          >
            Sports
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
