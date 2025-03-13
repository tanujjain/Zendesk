import opik

# Azure llm pricing
INPUT_TOKEN_PER_MIL = 2.5 # 2.5 usd per 1M input tokens (Using Azure Openai pricing from [here](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/)
OUTPUT_TOKEN_PER_MIL = 10 # 10 usd per 1M output tokens

client = opik.Opik()


if __name__ == '__main__':
    trace_list = client.search_traces(project_name="Default project", max_results=1000000)

    total_costs = 0
    cost_per_trace = []


    for trace in trace_list:
        try:
            input_token_costs = trace.usage['prompt_tokens'] * INPUT_TOKEN_PER_MIL / 1e6
            output_token_costs = trace.usage['completion_tokens'] * OUTPUT_TOKEN_PER_MIL / 1e6
            total_costs += input_token_costs + output_token_costs
            cost_per_trace.append(input_token_costs + output_token_costs)
        except:
            pass

    print(f"Total costs: {total_costs}")
    print(f"Average Cost per trace: {sum(cost_per_trace)/len(cost_per_trace)}")