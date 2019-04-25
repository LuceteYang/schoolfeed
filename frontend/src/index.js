import React, {Component} from 'react';
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { ConnectedRouter } from "connected-react-router";
import store, { history } from "redux/configureStore";
import App from "components/App";

const BoundaryHOC = ProtectedComponent =>
  class Boundary extends Component {
    state = {
      hasError: false
    };
    componentDidCatch = () => {
      this.setState({
        hasError: true
      });
    };
    render() {
      const { hasError } = this.state;
      if (hasError) {
        return <ErrorFallback />;
      } else {
        return <ProtectedComponent />;
      }
    }
  };

const PErrorMaker = BoundaryHOC(App);
const ErrorFallback = () => "Sorry something went wrong";

ReactDOM.render(

	<Provider store={store}>
		<ConnectedRouter history={history}>
			<PErrorMaker />
    	</ConnectedRouter>
	</Provider>, 
  document.getElementById("root")
);
