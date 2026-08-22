import argparse
from application.orchestrator import run

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--full-assessment', action='store_true')
    args = parser.parse_args()

    if args.full_assessment:
        run()
    else:
        print('Use --full-assessment')

if __name__ == '__main__':
    main()
