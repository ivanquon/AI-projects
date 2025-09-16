import "./App.css";
import Header from "./components/Header";
import Chatbox from "./components/Chatbox";
import DatabaseButtons from "./components/DatabaseButtons";
import { ThemeProvider } from "@mui/material";
import { theme } from "./theme";

function App() {
    return (
        <ThemeProvider theme={theme}>
            <Header />
            <Chatbox />
            <DatabaseButtons />
        </ThemeProvider>
    );
}

export default App;
