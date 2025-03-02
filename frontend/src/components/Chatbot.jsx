import React, { useState } from "react";

const Chatbot = () => {
    const [query, setQuery] = useState("");
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        if (!query) return;
        setLoading(true);

        try {
            const res = await fetch(`http://127.0.0.1:8000/chat?query=${encodeURIComponent(query)}`);
            const data = await res.json();
            setResponse(data);
        } catch (error) {
            console.error("Error fetching chatbot response:", error);
        }
        setLoading(false);
    };

    return (
        <div className="chat-container">
            <h2>AI-Powered E-Commerce Chatbot</h2>
            <div className="chat-box">
                {response && (
                    <div className="bot-response">
                        <p><strong>🤖 Chatbot:</strong> {response.response}</p>
                        <h4>🔍 Recommended Products:</h4>
                        <ul>
                            {response.results.map((product, index) => (
                                <li key={index}>
                                    {/* <p>{product.image}</p> */}
                                    <img src={product.image} alt={product.name} width="100" />
                                    {/* <img src={`https://api.codetabs.com/v1/proxy?quest=${encodeURIComponent(product.image)}`} alt={product.name} width="100" /> */}
                                    <p><strong>{product.name}</strong></p>
                                    <p>Price: {product.price} MKD</p>
                                    <a href={product.link} target="_blank" rel="noopener noreferrer">🔗 View Product</a>
                                </li>
                            ))}
                        </ul>
                    </div>
                )}
            </div>
            <div className="input-section">
                <input 
                    type="text" 
                    value={query} 
                    onChange={(e) => setQuery(e.target.value)} 
                    placeholder="Ask me about a product..."
                />
                <button onClick={handleSearch} disabled={loading}>
                    {loading ? "Searching..." : "Search"}
                </button>
            </div>
        </div>
    );
};

export default Chatbot;
