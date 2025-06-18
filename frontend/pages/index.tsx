import React from 'react';
import Head from 'next/head';
import FileUpload from '../components/FileUpload';
import ChatInterface from '../components/ChatInterface';

const Home: React.FC = () => {
  return (
    <div>
      <Head>
        <title>Financial Statement Q&A</title>
        <meta name="description" content="Ask questions about financial statements" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1 className="mainTitle">Financial Statement Q&A System</h1>
        <div className="mainContainer">
          <div className="card uploadCard">
            <h2 className="sectionTitle">Upload Financial Statement</h2>
            <FileUpload />
          </div>
          <div className="card chatCard">
            <h2 className="sectionTitle">Ask Questions</h2>
            <ChatInterface />
          </div>
        </div>
      </main>

      <footer style={{ textAlign: 'center', padding: '1rem', marginTop: '2rem' }}>
        <p style={{ color: '#e0e0e0' }}>Powered by RAG Technology</p>
      </footer>
    </div>
  );
};

export default Home; 