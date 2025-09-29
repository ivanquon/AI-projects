import { Box, Button, Grid, List, ListItem, ListItemText } from "@mui/material"
import { useState } from "react"
import AddSourceDialog from "./AddSourceDialog"

const BACKEND_URL = import.meta.env.BACKEND_URL

export default function DatabaseButtons() {
    const [sources, setSources] = useState<string[]>([])

    const fetchSources = async () => {
        const res = await fetch(`${BACKEND_URL}/sources`)
        const sources = await res.json()
        setSources(sources)
        console.log(sources)
    }

    const deleteSources = async () => {
        await fetch(`${BACKEND_URL}/sources`, {
            method: "DELETE",
        })
    }

    const addSource = async (source: string) => {
        await fetch(`${BACKEND_URL}/sources/wikipedia`, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                source: source,
            }),
        })
    }

    return (
        <Grid container spacing={2}>
            <Grid size={4}>
                <Button onClick={fetchSources}>View All Sources</Button>
            </Grid>
            <Grid size={4}>
                <AddSourceDialog onSubmit={addSource} />
            </Grid>
            <Grid size={4}>
                <Button onClick={deleteSources}>Delete All Sources</Button>
            </Grid>
            <Grid size={12}>
                <Box>
                    <List
                        sx={{
                            height: "10vh",
                            border: "1px solid grey",
                            overflowY: "auto",
                        }}
                    >
                        {sources.map((item, index) => {
                            return (
                                <ListItem
                                    key={index}
                                    sx={{
                                        whiteSpace: "normal",
                                        wordBreak: "break-word", // to break long words if needed
                                        py: 0,
                                    }}
                                >
                                    <ListItemText>
                                        {index + 1}. {item}
                                    </ListItemText>
                                </ListItem>
                            )
                        })}
                    </List>
                </Box>
            </Grid>
        </Grid>
    )
}
