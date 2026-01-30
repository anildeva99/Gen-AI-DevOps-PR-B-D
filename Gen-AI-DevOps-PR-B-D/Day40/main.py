
m agent import agent

def main():
        print("Enter your question:")
            question = input("> ")

                response = agent.run(question)
                    print("\nAgent Response:\n", response)

                    if __name__ == "__main__":
                            main()

