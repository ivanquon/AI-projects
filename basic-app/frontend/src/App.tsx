import "./App.css";
import Header from "./components/Header";
import Chatbox from "./components/Chatbox";
import DatabaseButtons from "./components/DatabaseButtons";

function App() {
  return (
    <div>
      <Header />
      <Chatbox />
      <DatabaseButtons />
    </div>
  );
}

export default App;
