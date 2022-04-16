import React from "react";
import {
  AppBar,
  Toolbar,
  CssBaseline,
  Typography,
  makeStyles,
} from "@mui/material";

const useStyles = makeStyles((theme) => ({
  navlinks: {
    marginLeft: theme.spacing(10),
    display: "flex",
  },
 logo: {
    flexGrow: "1",
    cursor: "pointer",
  },
  link: {
    textDecoration: "none",
    color: "white",
    fontSize: "20px",
    marginLeft: theme.spacing(20),
    "&:hover": {
      color: "yellow",
      borderBottom: "1px solid white",
    },
  },
}));

function Navbar() {
  const classes = useStyles();

  return (
    <AppBar position="static">
      <CssBaseline />
      <Toolbar>
        <Typography variant="h4" className={classes.logo}>
          Navbar
        </Typography>
          <div className={classes.navlinks}>
            <a to="/" className={classes.link}>
              Home
            </a>
            <a to="/about" className={classes.link}>
              About
            </a>
            <a to="/contact" className={classes.link}>
              Contact
            </a>
            <a to="/faq" className={classes.link}>
              FAQ
            </a>
          </div>
      </Toolbar>
    </AppBar>
  );
}
export default Navbar;