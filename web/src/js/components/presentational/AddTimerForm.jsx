import React, { Component } from "react";
import PropTypes from "prop-types";
import { Card, Form, Button, Input, Dropdown} from "semantic-ui-react";

const AddTimerForm = ({ cancel, submit, timeChanged, processSelected, allProcesses }) => {
		return (
			<Card>
				<Card.Content>
					<Form>
						<Form.Field>
							<label>Time</label>
							<Input type="time" onChange={timeChanged} />
						</Form.Field>
						<Form.Field>
							<label>Process</label>
							<Dropdown selection 
								onChange={processSelected} 
								placeholder='Select the process' 
								options={allProcesses} />
						</Form.Field>
						<Button.Group>
						<Button negative onClick={cancel}>Cancel</Button>
						<Button.Or />
						<Button type="submit" positive onClick={submit}>Submit</Button>
						</Button.Group>
					</Form>
				</Card.Content>
			</Card>
		);
};

AddTimerForm.propTypes = {
	cancel: PropTypes.func.isRequired,
	submit: PropTypes.func.isRequired,
	timeChanged: PropTypes.func.isRequired,
	processSelected: PropTypes.func.isRequired,
	allProcesses: PropTypes.array.isRequired
};
export default AddTimerForm;
