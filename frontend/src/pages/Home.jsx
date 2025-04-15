import React from 'react';
import { getAuth } from 'firebase/auth';

const wrapper = "min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-white flex flex-col justify-center items-center px-4 py-10";
const container = "max-w-2xl text-center space-y-6";
const heading = "text-4xl font-bold";
const subText = "text-lg text-gray-600 dark:text-gray-300";
const buttonWrapper = "mt-8";
const buttonStyle = "px-6 py-3 bg-green-600 text-white rounded hover:bg-green-700 transition focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-50";

const Home = () => {
  const auth = getAuth();
  const user = auth.currentUser;

  return (
    <div className={wrapper}>
      <div className={container}>
        <h1 className={heading}>
          Welcome{user ? `, ${user.displayName || 'Valued User'}` : ''} 👋
        </h1>

        <p className={subText}>
          Segment Indian language text with gender-aware, context-rich logic. Start with free text or upload a PDF.
        </p>

        <div className={buttonWrapper}>
          <a 
            href="https://segmenterhindi.streamlit.app/" 
            target="_blank" 
            rel="noopener noreferrer"
          >
            <button
              className={buttonStyle}
              title="Go to Segmenter App"
              aria-label="Go to Segmenter App"
            >
              Go to Segmenter
            </button>
          </a>
        </div>
      </div>
    </div>
  );
};

export default Home;
