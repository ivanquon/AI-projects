import { createTheme } from "@mui/material";

export const theme = createTheme({
    palette: {
        mode: "light", // or 'dark'
        primary: {
            main: "#000000", // Black
            contrastText: "#ffffff", // Text on black
        },
        secondary: {
            main: "#ffffff", // White
            contrastText: "#000000", // Text on white
        },
        background: {
            default: "#ffffff", // Page background
            paper: "#f0f0f0", // Card or surface background
        },
        text: {
            primary: "#000000",
            secondary: "#444444",
        },
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {},
            },
            defaultProps: {
                variant: "outlined",
            },
        },
        MuiList: {
            styleOverrides: {
                root: { borderRadius: 8, border: "1px solid grey" },
            },
        },
        MuiGrid: {
            styleOverrides: {
                root: {
                    alignContent: "center",
                },
            },
        },
    },
});
