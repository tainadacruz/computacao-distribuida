import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [tupleData, setTupleData] = useState('');
  const [searchedTuple, setSearchedTuple] = useState('');
  const [result, setResult] = useState('');
  const [tuples, setTuples] = useState([]);

  const handleWriteTuple = async () => {
    try {
      const response = await axios.post('http://localhost:5000/write_tuple', { tuple_data: tupleData });
      alert(response.data.message);
      fetchTuples();
    } catch (error) {
      console.error('Error writing tuple:', error);
    }
  };

  const handleGetTuple = async () => {
    try {
      const response = await axios.post('http://localhost:5000/get_tuple', { searched_tuple: searchedTuple });
      setResult(response.data.tuple || response.data.message);
      fetchTuples();
    } catch (error) {
      console.error('Error getting tuple:', error);
    }
  };

  const fetchTuples = async () => {
    try {
      const response = await axios.get('http://localhost:5000/list_tuples');
      setTuples(response.data.tuples || []);
    } catch (error) {
      console.error('Error listing tuples:', error);
    }
  };

  useEffect(() => {
    fetchTuples();
  }, []);

  return (
    <div className="App">
    <h1>Tuple Space</h1>
    <div>
    <h2>Write Tuple</h2>
    <input
    type="text"
    value={tupleData}
    onChange={(e) => setTupleData(e.target.value)}
    placeholder="Enter tuple data"
    />
    <button onClick={handleWriteTuple}>Write</button>
    </div>
    <div>
    <h2>Get Tuple</h2>
    <input
    type="text"
    value={searchedTuple}
    onChange={(e) => setSearchedTuple(e.target.value)}
    placeholder="Enter tuple pattern"
    />
    <button onClick={handleGetTuple}>Get</button>
    {result && <p>Result: {result}</p>}
    </div>
    <div>
    <h2>List Tuples</h2>
    <button onClick={fetchTuples}>Refresh</button>
    <ul>
    {tuples.map((tuple, index) => (
      <li key={index}>{tuple}</li>
    ))}
    </ul>
    </div>
    </div>
  );
}

export default App;
