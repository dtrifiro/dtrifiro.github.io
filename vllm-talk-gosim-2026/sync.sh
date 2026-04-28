rsync --exclude-from=<(printf "node_modules
.git
memory.md
gosim_talk.md
") -aP vllm-talk/ dtrifiro.github.io/vllm-talk-gosim-2026
