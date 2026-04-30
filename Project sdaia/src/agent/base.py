import time
import hashlib


class BaseAgent:
    def __init__(self, llm, tools, prompt, max_steps: int = 10, verbose: bool = True):
        self.llm = llm
        self.tools = tools
        self.prompt = prompt
        self.max_steps = max_steps
        self.verbose = verbose

        self.seen_responses = set()
        self.seen_observations = set()

    def _hash(self, text: str):
        return hashlib.md5(text.encode()).hexdigest()

    def run(self, user_input: str):
        observation = user_input

        start_time = time.time()
        tool_logs = []

        for step in range(self.max_steps):

            step_start = time.time()

            full_prompt = f"""
{self.prompt}

INPUT:
{observation}
"""

            response = self.llm.invoke(full_prompt)

            step_time = time.time() - step_start

            if self.verbose:
                print(f"\n[STEP {step}] ({step_time:.2f}s)\n{response}\n")

            #  LOOP DETECTION (RESPONSE)
            resp_hash = self._hash(response)

            if resp_hash in self.seen_responses:
                return {
                    "final": "Stopped: repeated response detected",
                    "steps": step + 1,
                    "total_time_sec": round(time.time() - start_time, 2),
                    "tool_logs": tool_logs
                }

            self.seen_responses.add(resp_hash)

            #  FINAL STOP
            if response.strip().startswith("FINAL"):
                return {
                    "final": response,
                    "steps": step + 1,
                    "total_time_sec": round(time.time() - start_time, 2),
                    "tool_logs": tool_logs
                }

            #  ACTION HANDLER (TOOLS)
            if "ACTION:" in response:

                tool_name, tool_input = self._parse_action(response)

                if tool_name == "read_file":
                    if not tool_input.startswith("src/"):
                        tool_input = "src/" + tool_input

                # execute tool
                if tool_name in self.tools:
                    result = self.tools[tool_name](tool_input)
                else:
                    result = f"ERROR: Tool not found -> {tool_name}"

                tool_logs.append({
                    "tool": tool_name,
                    "input": tool_input,
                    "output": result
                })

                #  FIX: OBSERVATION LOOP PREVENTION
                new_observation = f"""
TOOL RESULT:
{result}

Use this information. Do NOT repeat previous results.
"""

                obs_hash = self._hash(new_observation)

                if obs_hash in self.seen_observations:
                    new_observation = "NEW INFORMATION ONLY - CONTINUE REASONING WITHOUT REPETITION"

                self.seen_observations.add(obs_hash)

                observation = new_observation

                continue

        
        return {
            "final": "Stopped: max steps reached",
            "steps": self.max_steps,
            "total_time_sec": round(time.time() - start_time, 2),
            "tool_logs": tool_logs
        }

    def _parse_action(self, text: str):
        """
        Expected format:
        ACTION: read_file
        INPUT: data.txt
        """

        tool_name = ""
        tool_input = ""

        for line in text.split("\n"):
            line = line.strip()

            if line.startswith("ACTION:"):
                tool_name = line.replace("ACTION:", "").strip()

            if line.startswith("INPUT:"):
                tool_input = line.replace("INPUT:", "").strip()

        return tool_name, tool_input